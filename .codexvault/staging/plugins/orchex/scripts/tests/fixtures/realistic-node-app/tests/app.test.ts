import { describe, expect, it } from "vitest";
import { greet } from "../src/app";

describe("greet", () => {
    it("formats the greeting", () => {
        expect(greet("Orchex")).toBe("Hello, Orchex");
    });
});
