import { spawnSync } from "node:child_process";

const userArgs = process.argv.slice(2);

const candidates =
  process.platform === "win32"
    ? [
        ["python3", userArgs],
        ["py", ["-3.14", ...userArgs]],
        ["py", ["-3.12", ...userArgs]],
        ["py", userArgs],
        ["python", userArgs],
      ]
    : [
        ["python3", userArgs],
        ["python", userArgs],
      ];

for (const [command, args] of candidates) {
  const probeArgs =
    command === "py" && args[0]?.startsWith("-")
      ? [args[0], "--version"]
      : ["--version"];
  const probe = spawnSync(command, probeArgs, { stdio: "ignore" });

  if (probe.error || probe.status !== 0) {
    continue;
  }

  const result = spawnSync(command, args, { stdio: "inherit" });

  if (result.status === 0) {
    process.exit(result.status ?? 0);
  }

  process.exit(result.status ?? 1);
}

console.error("Unable to find a usable Python interpreter.");
process.exit(1);
