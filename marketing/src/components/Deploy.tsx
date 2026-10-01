import { Terminal, Settings, Palette, Globe } from 'lucide-react';

const deployFeatures = [
  {
    icon: Terminal,
    title: 'One-Command Deploy',
    description: 'Single docker command spins up everything',
  },
  {
    icon: Settings,
    title: 'Configure Don\'t Code',
    description: 'Modify config files, not source code',
  },
  {
    icon: Palette,
    title: 'White-Label Ready',
    description: 'Rebrand and resell as your own',
  },
  {
    icon: Globe,
    title: 'Deploy Anywhere',
    description: 'Any Docker host — cloud or on-premise',
  },
];

export function Deploy() {
  const scrollToPricing = () => {
    const element = document.querySelector('#pricing');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="deploy" className="py-20 md:py-32 bg-surface">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-exo font-black text-3xl md:text-4xl lg:text-5xl text-text">
            Go Live in One Command.
          </h2>
          <p className="mt-4 text-lg md:text-xl text-primary/70 max-w-2xl mx-auto">
            No DevOps required. If you can run a terminal command, you can deploy Kavaro.
          </p>
        </div>

        <div className="max-w-4xl mx-auto mb-12">
          <div className="bg-[#0F0F1A] rounded-2xl overflow-hidden shadow-xl">
            <div className="flex items-center gap-2 px-4 py-3 bg-[#1E2128]">
              <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
              <span className="ml-4 text-white/40 text-sm font-mono">terminal</span>
            </div>
            <div className="p-6 font-mono text-sm md:text-base overflow-x-auto">
              <div className="space-y-2">
                <div>
                  <span className="text-green-400">$</span>
                  <span className="text-white ml-2">git clone https://github.com/92eleven/Kavaro.git </span>
                  <span className="text-accent/80">&& cd Kavaro</span>
                </div>
                <div>
                  <span className="text-green-400">$</span>
                  <span className="text-white ml-2">cp .env.example .env </span>
                  <span className="text-accent/80">&& nano .env</span>
                </div>
                <div>
                  <span className="text-green-400">$</span>
                  <span className="text-white ml-2">nano knowledge_base.json</span>
                </div>
                <div>
                  <span className="text-green-400">$</span>
                  <span className="text-white ml-2">docker compose up -d</span>
                </div>
                <div>
                  <span className="text-green-400">$</span>
                  <span className="text-white ml-2">curl http://localhost:8080/health</span>
                </div>
                <div className="mt-4 text-green-400">
                  {`{"status": "healthy", "agent": "kavaro", "version": "1.0.0"}`}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {deployFeatures.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-6 text-center shadow-sm"
            >
              <div className="w-12 h-12 mx-auto bg-accent/10 rounded-xl flex items-center justify-center mb-3">
                <feature.icon className="w-6 h-6 text-accent" />
              </div>
              <h3 className="font-exo font-bold text-text">{feature.title}</h3>
              <p className="text-primary/60 text-sm mt-1">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="bg-accent/5 border border-accent/20 rounded-2xl p-6 md:p-8 text-center mb-10">
          <p className="text-primary/80 text-lg">
            From <span className="font-bold">git clone</span> to a live qualifying agent — average setup time <span className="text-accent font-bold">under 5 minutes</span>.
          </p>
        </div>

        <div className="text-center">
          <button
            onClick={scrollToPricing}
            className="px-10 py-4 bg-accent text-primary font-bold text-lg rounded-xl hover:bg-accent/90 transition-all shadow-lg hover:shadow-xl hover:scale-105"
          >
            Deploy Kavaro Today
          </button>
        </div>
      </div>
    </section>
  );
}
