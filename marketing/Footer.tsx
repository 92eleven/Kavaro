export function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-text py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">
          <div onClick={scrollToTop} className="cursor-pointer">
            <span className="font-exo font-black text-3xl" style={{ transform: 'skewX(-22deg)', display: 'inline-block' }}>
              <span className="text-accent">K</span>
              <span className="text-white">AVARO</span>
            </span>
            <p className="text-white/60 mt-2">Your 24/7 Lead Qualification Engine</p>
          </div>

          <div className="flex flex-wrap gap-8">
            <button onClick={() => scrollToSection('#features')} className="text-white/60 hover:text-accent transition-colors font-medium">Features</button>
            <button onClick={() => scrollToSection('#how-it-works')} className="text-white/60 hover:text-accent transition-colors font-medium">How It Works</button>
            <button onClick={() => scrollToSection('#integrations')} className="text-white/60 hover:text-accent transition-colors font-medium">Integrations</button>
            <button onClick={() => scrollToSection('#pricing')} className="text-white/60 hover:text-accent transition-colors font-medium">Pricing</button>
            <button onClick={() => scrollToSection('#contact')} className="text-white/60 hover:text-accent transition-colors font-medium">Contact</button>
          </div>
        </div>

        <div className="border-t border-white/10 mt-12 pt-8 text-center">
          <p className="text-white/40 text-sm">© 2026 Kavaro. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
