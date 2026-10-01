import { TrendingUp, Wrench, FileText, Target } from 'lucide-react';

const steps = [
  {
    icon: TrendingUp,
    title: '7-Day Rolling Analysis',
    description: 'Every conversation is logged and analyzed weekly to identify patterns and improvement opportunities.',
  },
  {
    icon: Wrench,
    title: 'Automatic Prompt Optimization',
    description: 'The system refines its own prompts based on conversion outcomes, getting sharper with each cycle.',
  },
  {
    icon: FileText,
    title: 'Full Audit Trail',
    description: 'Complete visibility into every interaction — what was asked, how leads responded, and outcomes.',
  },
  {
    icon: Target,
    title: 'Conversion-Focused',
    description: 'Self-improvement is measured against real conversions, not vanity metrics.',
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 md:py-32 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-exo font-black text-3xl md:text-4xl lg:text-5xl text-text">
            It Gets Smarter Every Single Interaction.
          </h2>
          <p className="mt-4 text-lg md:text-xl text-primary/70">
            Most AI tools stay the same. Kavaro improves automatically.
          </p>
        </div>

        <div className="mb-16">
          <div className="flex flex-wrap justify-center items-center gap-3 md:gap-4">
            {['Lead Interaction', 'Outcome Logged', '7-Day Analysis', 'Prompt Refined', 'Better Next Time'].map((step, index) => (
              <div key={index} className="flex items-center">
                <div className="bg-primary text-white px-4 py-2 md:px-6 md:py-3 rounded-lg font-semibold text-sm md:text-base">
                  {step}
                </div>
                {index < 4 && (
                  <div className="hidden md:block mx-2">
                    <svg className="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="md:hidden mt-4 text-center">
            <div className="inline-flex flex-col gap-1">
              {[0, 1, 2, 3].map((i) => (
                <div key={i} className="inline-block mx-auto">
                  <svg className="w-5 h-5 text-accent rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <div
              key={index}
              className="bg-surface rounded-2xl p-6 text-center"
            >
              <div className="w-14 h-14 mx-auto bg-accent/10 rounded-xl flex items-center justify-center mb-4">
                <step.icon className="w-7 h-7 text-accent" />
              </div>
              <h3 className="font-exo font-bold text-lg text-text mb-2">{step.title}</h3>
              <p className="text-primary/70 text-sm">{step.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-text rounded-2xl p-6 md:p-8 text-center">
          <p className="text-white/90 text-lg md:text-xl leading-relaxed">
            Kavaro that learns from 100 conversations is measurably more effective than Kavaro on day one. Your qualification accuracy <span className="text-accent font-semibold">compounds over time</span> — and so does your revenue.
          </p>
        </div>
      </div>
    </section>
  );
}
