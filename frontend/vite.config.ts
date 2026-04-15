import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { defineConfig } from "vite";

const nodeModules = path.resolve(__dirname, "node_modules");

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
    fs: {
      allow: [".."],
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test-setup.ts"],
    include: ["../tests/frontend/**/*.test.{ts,tsx}"],
    css: false,
    alias: {
      "react/jsx-dev-runtime": path.join(nodeModules, "react/jsx-dev-runtime"),
      "react/jsx-runtime": path.join(nodeModules, "react/jsx-runtime"),
      "react-dom/client": path.join(nodeModules, "react-dom/client"),
      "react-dom": path.join(nodeModules, "react-dom"),
      react: path.join(nodeModules, "react"),
      "@testing-library/react": path.join(nodeModules, "@testing-library/react"),
      "@testing-library/jest-dom/vitest": path.join(nodeModules, "@testing-library/jest-dom/vitest"),
      "@testing-library/jest-dom": path.join(nodeModules, "@testing-library/jest-dom"),
      "@testing-library/user-event": path.join(nodeModules, "@testing-library/user-event"),
      "lucide-react": path.join(nodeModules, "lucide-react"),
    },
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/main.tsx", "src/test-setup.ts"],
    },
  },
});
