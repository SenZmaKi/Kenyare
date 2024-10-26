import { execSync } from "child_process";

const [, , ...args] = process.argv;

execSync(`npm ${args.join(" ")}`, { windowsHide: true, stdio: "inherit" });
