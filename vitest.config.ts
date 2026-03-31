import path from "node:path";
import { defineConfig } from "vitest/config";

const resolveFromRoot = (value: string) => path.resolve(__dirname, value);

export default defineConfig({
  resolve: {
    alias: {
      "@eidos/shared-types": resolveFromRoot("packages/shared-types/src/index.ts"),
      "@eidos/shared-ui": resolveFromRoot("packages/shared-ui/src/index.ts"),
      "@eidos/analytics": resolveFromRoot("packages/analytics/src/index.ts")
    }
  },
  test: {
    projects: [
      {
        test: {
          name: "desktop",
          include: ["apps/desktop/**/*.{test,spec}.tsx"],
          environment: "jsdom",
          globals: true,
          setupFiles: ["apps/desktop/src/test/setup.ts"]
        }
      },
      {
        test: {
          name: "packages",
          include: ["packages/**/*.{test,spec}.ts"],
          environment: "node",
          globals: true
        }
      }
    ],
    globals: true
  }
});
