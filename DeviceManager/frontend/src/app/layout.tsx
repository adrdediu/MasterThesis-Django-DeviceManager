'use client'

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { useEffect } from "react";
import { initializeDjangoContext, useDjangoContext } from "./utils/djangoContext";
const inter = Inter({ subsets: ["latin"] });

import { ThemeProvider } from "./components/theme-provider"
import { ModeToggle } from './components/mode-toggle'; // Import your mode toggle component

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  useEffect(() => {

    initializeDjangoContext();
  }, []);

  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <ModeToggle />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
