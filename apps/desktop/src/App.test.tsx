import { render, screen } from "@testing-library/react";

import { App } from "./App";

describe("App", () => {
  it("renders the foundation shell", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", {
        name: /desktop-first portfolio intelligence/i,
      })
    ).toBeInTheDocument();
    expect(
      screen.getByText(/shared logic: analytics and cross-surface types/i)
    ).toBeInTheDocument();
    expect(screen.getByText("http://127.0.0.1:8000")).toBeInTheDocument();
  });
});
