import { Sparkles, Zap, ShieldCheck } from 'lucide-react';

export function Hero() {
  const scrollToPricing = () => {
    const element = document.querySelector('#pricing');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="pt-32 md:pt-40 pb-20 md:pb-32 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="font-exo font-black text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-text leading-tight">
            Your <span className="text-deep-accent">24/7</span> Lead<br />Qualification Engine
          </h1>

          <p className="mt-6 md:mt-8 max-w-3xl mx-auto text-lg md:text-xl text-primary/70 leading-relaxed">
            Kavaro is an autonomous AI agent that qualifies inbound leads and books appointments — automatically, instantly, and around the clock. No more missed leads. No more manual screening. No more prospects slipping through the cracks.
          </p>

          <div className="mt-10 md:mt-12 flex flex-wrap justify-center gap-4 md:gap-8">
            <div className="flex items-center gap-2 px-4 py-2 bg-deep-accent/10 rounded-full border border-deep-accent/30">
              <Sparkles className="w-5 h-5 text-deep-accent" />
              <span className="font-semibold text-deep-accent">24/7 Always On</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-deep-accent/10 rounded-full border border-deep-accent/30">
              <Zap className="w-5 h-5 text-deep-accent" />
              <span className="font-semibold text-deep-accent">&lt;30s Response Time</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-deep-accent/10 rounded-full border border-deep-accent/30">
              <ShieldCheck className="w-5 h-5 text-deep-accent" />
              <span className="font-semibold text-deep-accent">100% Leads Captured</span>
            </div>
          </div>

          <div className="mt-10 md:mt-12">
            <button
              onClick={scrollToPricing}
              className="px-8 py-4 bg-accent text-primary font-bold text-lg rounded-xl hover:bg-accent/90 transition-all shadow-lg hover:shadow-xl hover:scale-105"
            >
              Deploy Kavaro Today
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
