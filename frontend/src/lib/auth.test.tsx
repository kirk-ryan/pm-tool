import { renderHook, act } from "@testing-library/react";
import type { ReactNode } from "react";
import { AuthProvider, useAuth } from "@/lib/auth";

const wrapper = ({ children }: { children: ReactNode }) => (
  <AuthProvider>{children}</AuthProvider>
);

beforeEach(() => {
  sessionStorage.clear();
});

describe("useAuth", () => {
  it("is unauthenticated after checking empty storage", () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(result.current.isAuthenticated).toBe(false);
  });

  it("login with correct credentials returns true and sets auth", () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    let success!: boolean;
    act(() => {
      success = result.current.login("user", "password");
    });
    expect(success).toBe(true);
    expect(result.current.isAuthenticated).toBe(true);
    expect(sessionStorage.getItem("kanban_auth")).toBe("true");
  });

  it("login with wrong credentials returns false and stays unauthenticated", () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    let success!: boolean;
    act(() => {
      success = result.current.login("admin", "wrongpassword");
    });
    expect(success).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it("login rejects wrong password for valid username", () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    let success!: boolean;
    act(() => {
      success = result.current.login("user", "wrong");
    });
    expect(success).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it("logout clears auth state and sessionStorage", () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    act(() => {
      result.current.login("user", "password");
    });
    act(() => {
      result.current.logout();
    });
    expect(result.current.isAuthenticated).toBe(false);
    expect(sessionStorage.getItem("kanban_auth")).toBeNull();
  });

  it("restores auth from sessionStorage on mount", () => {
    sessionStorage.setItem("kanban_auth", "true");
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(result.current.isAuthenticated).toBe(true);
  });

  it("throws if used outside AuthProvider", () => {
    expect(() => renderHook(() => useAuth())).toThrow(
      "useAuth must be used within AuthProvider"
    );
  });
});
