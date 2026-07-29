import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClaritFi — Know What You Owe Before You Sign",
  description: "Paste loan agreements or credit card terms to expose hidden charges, calculate the real APR, and translate complex legal jargon into plain language. Powered by AI.",
  icons: {
    icon: [
      { url: "/favicon.png", type: "image/png" },
      { url: "/icon.png", type: "image/png" },
    ],
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="min-h-full flex flex-col bg-[#070b13] text-slate-100 font-sans">
        {children}
      </body>
    </html>
  );
}
