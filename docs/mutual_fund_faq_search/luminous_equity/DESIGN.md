---
name: Luminous Equity
colors:
  surface: '#f9f9ff'
  surface-dim: '#d8d9e5'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3fe'
  surface-container: '#ecedf9'
  surface-container-high: '#e6e8f3'
  surface-container-highest: '#e0e2ed'
  on-surface: '#181c23'
  on-surface-variant: '#414755'
  inverse-surface: '#2d3039'
  inverse-on-surface: '#eef0fc'
  outline: '#717786'
  outline-variant: '#c1c6d7'
  surface-tint: '#005bc1'
  primary: '#0058bc'
  on-primary: '#ffffff'
  primary-container: '#0070eb'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#006a66'
  on-secondary: '#ffffff'
  secondary-container: '#61f5ed'
  on-secondary-container: '#006f6a'
  tertiary: '#6d37d3'
  on-tertiary: '#ffffff'
  tertiary-container: '#8654ee'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#65f8f0'
  secondary-fixed-dim: '#3fdbd4'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504d'
  tertiary-fixed: '#eaddff'
  tertiary-fixed-dim: '#d1bcff'
  on-tertiary-fixed: '#24005b'
  on-tertiary-fixed-variant: '#5715bd'
  background: '#f9f9ff'
  on-background: '#181c23'
  surface-variant: '#e0e2ed'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max-width: 1120px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  section-gap: 80px
---

## Brand & Style

The design system is engineered for a premium financial experience, blending Apple-inspired minimalism with a high-fidelity "Glassmorphic" aesthetic. It targets sophisticated investors who seek clarity and calm within complex financial data. 

The emotional response should be one of "effortless intelligence"—where the interface feels light, expensive, and precise. The design style utilizes a mix of **Minimalism** for layout and **Glassmorphism** for depth, using subtle background blurs and vibrant, narrow-spectrum glows to distinguish information layers without adding visual noise.

## Colors

The palette is anchored by a vibrant, "Electric Blue" primary color used for critical actions and navigational intent. To maintain a premium feel, the background is a textured off-white, preventing the starkness of pure hex white while allowing the pristine white surface containers to "pop" via elevation.

Gradients are used sparingly as accents (Teal to Purple) for thin borders or ambient background glows to suggest financial "growth" and "vibrancy." Warning states utilize a "Rich Amber" with a micro-gradient (e.g., #F59E0B to #D97706) to denote advisory caution without breaking the high-end aesthetic.

## Typography

This design system uses **Inter** exclusively to achieve a systematic, utilitarian, yet modern look. The hierarchy is established through significant weight contrast and negative letter-spacing on larger headings to create a "dense," premium editorial feel. 

Body text remains dark (#1A1A1A) for maximum legibility against white and frosted surfaces. Use `label-md` for metadata like fund categories or timestamping, ensuring the uppercase styling provides a clear visual anchor.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop to maintain a "contained" and curated feel, transitioning to a fluid model for mobile devices. 

- **Desktop:** 12-column grid, 1120px max-width, 24px gutters.
- **Tablet:** 8-column grid, 32px margins.
- **Mobile:** 4-column grid, 20px margins.

Whitespace is used as a structural element. Large section gaps (80px+) are encouraged to separate distinct FAQ categories, ensuring the user is never overwhelmed by information density.

## Elevation & Depth

Depth is the primary communicator of hierarchy in this design system. It uses three distinct tiers:

1.  **Base:** The off-white background (#F9F9FB).
2.  **Surface:** Pristine white containers with a subtle 1px border (#E5E7EB) and a soft, multi-layered shadow (0px 4px 20px rgba(0,0,0,0.03)).
3.  **Glass (Floating):** Floating elements (like search dropdowns or modals) use a `backdrop-blur` of 12px-20px and 80% opacity white.

**Ambient Glows:** Use low-opacity radial gradients (Teal #00C2BB at 5% opacity) positioned behind primary cards to create a "halo" effect, suggesting importance and high-value content.

## Shapes

The shape language is sophisticated and approachable. While the base `rounded-md` is 8px (0.5rem), the primary containers (Cards, Search Inputs) must use `rounded-xl` (24px) to achieve the signature premium look. 

Buttons should utilize a semi-pill shape (12px) to distinguish them from the larger container radii. Avoid sharp corners entirely to maintain the "soft" premium aesthetic.

## Components

### Search Bar
The central component of the application. It should be oversized (height: 64px), featuring a `rounded-xl` (24px) radius, a subtle 1px gradient border (Teal to Purple at 30% opacity), and a soft ambient shadow.

### Buttons
- **Primary:** Solid Vibrant Blue (#007AFF) with white text. High-gloss finish (subtle top-inner highlight).
- **Secondary:** Ghost style with a 1px border and a background blur when placed over glass surfaces.

### FAQ Cards
Cards should have a white background, 24px padding, and 24px border-radius. On hover, the border-color should shift to the primary blue, and the shadow should slightly deepen to simulate "lifting" toward the user.

### Advisory/Status Chips
Used for warnings or fund status. Use the Rich Amber palette with `label-sm` typography. The chip should have a 10% opacity fill of the amber color and a solid 1px border of the same hue to ensure it feels like a professional "advisory" rather than a generic error.

### Lists & Accordions
For FAQ answers, use clean dividers (1px, #F3F4F6). Expanding sections should use a smooth ease-in-out transition, pushing content down rather than overlapping, to respect the fluid whitespace.