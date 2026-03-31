import type { PropsWithChildren, ReactNode } from "react";

interface PanelProps extends PropsWithChildren {
  readonly eyebrow?: string;
  readonly title: string;
  readonly description?: ReactNode;
}

export function Panel({ eyebrow, title, description, children }: PanelProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="space-y-2">
        {eyebrow ? (
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            {eyebrow}
          </p>
        ) : null}
        <div className="space-y-1">
          <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
          {description ? (
            <div className="text-sm text-slate-600">{description}</div>
          ) : null}
        </div>
      </div>
      <div className="mt-4">{children}</div>
    </section>
  );
}
