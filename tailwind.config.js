/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: ["./src/**/*.{ts,tsx}"],
    theme: {
        container: {
            center: true,
            padding: "2rem",
            screens: {
                "2xl": "1400px",
            },
        },
        extend: {
            colors: {
                // 1. BRAND TOKENS (The identity)
                primary: {
                    DEFAULT: "#2563EB", // Royal Blue (Trustworthy)
                    foreground: "#FFFFFF",
                    subtle: "#EFF6FF", // Very light blue for backgrounds
                },

                // 2. SURFACE TOKENS (The layers)
                surface: {
                    DEFAULT: "#F8FAFC", // Slate 50 (App Background - not harsh white)
                    card: "#FFFFFF",    // White (Card Background)
                    hover: "#F1F5F9",   // Slate 100 (Clickable areas)
                },

                // 3. TEXT TOKENS (Readability)
                text: {
                    main: "#0F172A",    // Slate 900 (Headings, Values)
                    body: "#334155",    // Slate 700 (Paragraphs)
                    muted: "#64748B",   // Slate 500 (Labels, timestamps)
                    inverted: "#FFFFFF",
                },

                // 4. STATUS TOKENS (Data logic)
                status: {
                    success: "#16A34A", // Green 600
                    success_bg: "#DCFCE7",
                    warning: "#D97706", // Amber 600
                    warning_bg: "#FEF3C7",
                    error: "#DC2626",   // Red 600
                    error_bg: "#FEE2E2",
                },

                // Shadcn required mappings (simplified)
                border: "#E2E8F0",
                input: "#E2E8F0",
                ring: "#2563EB",
            },
            borderRadius: {
                lg: "0.75rem",    // 12px (Cards)
                xl: "1rem",       // 16px (Modals)
                full: "9999px",   // Buttons
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"], // Clean, legible
            }
        },
    },
    plugins: [require("tailwindcss-animate")],
}
