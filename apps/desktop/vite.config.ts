import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

const resolveFromRoot = (value: string) =>
  path.resolve(__dirname, "../..", value);

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@eidos/shared-types": resolveFromRoot(
        "packages/shared-types/src/index.ts"
      ),
      "@eidos/shared-ui": resolveFromRoot("packages/shared-ui/src/index.ts"),
      "@eidos/analytics": resolveFromRoot("packages/analytics/src/index.ts"),
    },
  },
});
