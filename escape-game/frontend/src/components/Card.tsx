import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
}

export function Card({ children, className = "", glow = false }: CardProps) {
  return (
    <div
      className={`${glow ? "panel-glow" : "panel"} p-5 ${className}`}
    >
      {children}
    </div>
  );
}

interface SectionTitleProps {
  title: string;
  subtitle?: string;
  icon?: string;
}

export function SectionTitle({ title, subtitle, icon }: SectionTitleProps) {
  return (
    <div className="mb-4">
      <h2 className="font-display font-bold text-sm uppercase tracking-widest text-neon-cyan flex items-center gap-2">
        {icon && <span aria-hidden>{icon}</span>}
        {title}
      </h2>
      {subtitle && (
        <p className="text-xs text-slate-500 mt-1">{subtitle}</p>
      )}
      <div className="mt-2 h-px bg-gradient-to-r from-neon-cyan/60 to-transparent" />
    </div>
  );
}
