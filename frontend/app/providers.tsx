"use client";

import { StackProvider } from "@stackframe/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <StackProvider
      projectId="your-project-id" // Replace with your actual project ID
      publishableClientKey="your-publishable-key" // Replace with your actual key
    >
      {children}
    </StackProvider>
  );
}
