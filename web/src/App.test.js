import { render, screen } from "@testing-library/react";
import App from "./App";

test("shows the login form when signed out", () => {
  localStorage.removeItem("authToken");
  render(<App />);
  expect(screen.getByRole("heading", { name: /login/i })).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
});
