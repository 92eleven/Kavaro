import { useState, useEffect } from 'react';

export function Navigation() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { href: '#features', label: 'Features' },
    { href: '#how-it-works', label: 'How It Works' },
    { href: '#integrations', label: 'Integrations' },
    { href: '#pricing', label: 'Pricing' },
    { href: '#contact', label: 'Contact' },
  ];

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        isScrolled ? 'bg-white/95 backdrop-blur-sm shadow-sm' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          <div className="flex items-center">
            <a href="#" className="flex items-center" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
              <span className="font-exo font-black text-2xl md:text-3xl" style={{ transform: 'skewX(-22deg)', display: 'inline-block' }}>
                <span className="text-accent">K</span>
                <span className="text-primary">AVARO</span>
              </span>
            </a>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <button
                key={link.href}
                onClick={() => scrollToSection(link.href)}
                className="text-primary hover:text-accent transition-colors font-medium"
              >
                {link.label}
              </button>
            ))}
            <button
              onClick={() => scrollToSection('#pricing')}
              className="px-6 py-2.5 bg-accent text-primary font-semibold rounded-lg hover:bg-accent/90 transition-all shadow-sm hover:shadow-md"
            >
              Deploy Kavaro Today
            </button>
          </div>

          <button
            className="md:hidden p-2 text-primary"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isMobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {isMobileMenuOpen && (
          <div className="md:hidden bg-white border-t">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => scrollToSection(link.href)}
                  className="block w-full text-left px-3 py-2 text-primary hover:text-accent hover:bg-surface rounded-lg transition-colors font-medium"
                >
                  {link.label}
                </button>
              ))}
              <button
                onClick={() => scrollToSection('#pricing')}
                className="block w-full mt-2 px-3 py-2 bg-accent text-primary font-semibold rounded-lg text-center"
              >
                Deploy Kavaro Today
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
