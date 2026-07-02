"""
Ingestion Pipeline Orchestrator
================================
Single entry point that runs the full ingestion pipeline:
  scrape → parse → chunk → embed

Designed to be invoked from GitHub Actions CI or locally:
  python -m backend.scripts.run_ingestion
"""

import sys
import time
import logging
from datetime import datetime, timezone

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ingestion")


def _banner(title: str) -> None:
    """Print a visual separator for CI log readability."""
    line = "═" * 60
    logger.info(line)
    logger.info(f"  {title}")
    logger.info(line)


def run_scraper() -> bool:
    """Phase 1A — Scrape Groww fund pages using Playwright."""
    _banner("STEP 1/4 · Web Scraping")
    try:
        from backend.scraper.scrape import scrape_pages
        scrape_pages()
        logger.info("Scraping completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Scraping failed: {e}", exc_info=True)
        return False


def run_parser() -> bool:
    """Phase 1B — Parse raw HTML into clean, section-tagged text."""
    _banner("STEP 2/4 · Document Parsing")
    try:
        from backend.ingestion.parser import main as parse_main
        parse_main()
        logger.info("Parsing completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Parsing failed: {e}", exc_info=True)
        return False


def run_chunker() -> bool:
    """Phase 1C — Split parsed documents into retrieval-friendly chunks."""
    _banner("STEP 3/4 · Chunking")
    try:
        from backend.ingestion.chunker import main as chunk_main
        chunk_main()
        logger.info("Chunking completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Chunking failed: {e}", exc_info=True)
        return False


def run_embedder() -> bool:
    """Phase 1D — Embed chunks with BGE and store in ChromaDB."""
    _banner("STEP 4/4 · Embedding & Indexing")
    try:
        from backend.ingestion.embedder import embed_and_store, verify_index
        embed_and_store()
        verify_index()
        logger.info("Embedding and indexing completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Embedding/indexing failed: {e}", exc_info=True)
        return False


def main() -> None:
    """Run the full ingestion pipeline end-to-end."""
    start_time = time.time()
    start_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    logger.info("")
    _banner(f"INGESTION PIPELINE · Started at {start_ts}")
    logger.info("")

    # ── Pipeline steps ─────────────────────────────────────────────────────
    steps = [
        ("Scraping", run_scraper),
        ("Parsing", run_parser),
        ("Chunking", run_chunker),
        ("Embedding", run_embedder),
    ]

    results = {}
    failed = False

    for name, step_fn in steps:
        step_start = time.time()
        success = step_fn()
        elapsed = time.time() - step_start
        results[name] = {"success": success, "elapsed": elapsed}

        if not success:
            failed = True
            # Scraping failure is non-fatal if we still have cached HTML from
            # a previous run — the parser can work with existing raw_html/.
            # But if parsing/chunking/embedding fails, we must abort.
            if name != "Scraping":
                logger.error(f"Pipeline aborted at '{name}' step.")
                break
            else:
                logger.warning(
                    "Scraping had errors. Continuing with existing raw HTML if available..."
                )

    # ── Summary ────────────────────────────────────────────────────────────
    total_elapsed = time.time() - start_time
    logger.info("")
    _banner("PIPELINE SUMMARY")

    for name, result in results.items():
        status = "✅ OK" if result["success"] else "❌ FAILED"
        logger.info(f"  {name:12s} → {status}  ({result['elapsed']:.1f}s)")

    logger.info(f"\n  Total time: {total_elapsed:.1f}s")

    # ── Exit code ──────────────────────────────────────────────────────────
    # We consider the pipeline successful if parsing, chunking, and embedding
    # all succeeded (scraping partial failure is tolerable).
    critical_failure = any(
        not results.get(step, {}).get("success", False)
        for step in ["Parsing", "Chunking", "Embedding"]
        if step in results
    )

    if critical_failure:
        logger.error("Ingestion pipeline FAILED with critical errors.")
        sys.exit(1)
    elif failed:
        logger.warning("Ingestion pipeline completed with warnings (scraping had errors).")
        sys.exit(0)
    else:
        logger.info("Ingestion pipeline completed successfully. ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
