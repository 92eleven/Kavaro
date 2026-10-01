import { useState } from 'react';
import { LoadAnimation } from './components/LoadAnimation';
import { Navigation } from './components/Navigation';
import { Hero } from './components/Hero';
import { Features } from './components/Features';
import { HowItWorks } from './components/HowItWorks';
import { Integrations } from './components/Integrations';
import { Pricing } from './components/Pricing';
import { Deploy } from './components/Deploy';
import { Contact } from './components/Contact';
import { Footer } from './components/Footer';


function App() {
  const [isLoading, setIsLoading] = useState(true);

  const handleContactSubmit = async (data: { name: string; email: string; company: string; message: string }) => {
    const res = await fetch('https://kavaro-production.up.railway.app/webhook/gmail', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-QualifAI-Secret': 'kavaro2026',
      },
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        message: data.message,
      }),
    });

    if (!res.ok) throw new Error('Request failed');
  };

  return (
    <>
      {isLoading && <LoadAnimation onComplete={() => setIsLoading(false)} />}

      <div
        className={`transition-opacity duration-500 ${
          isLoading ? 'opacity-0' : 'opacity-100'
        }`}
      >
        <Navigation />
        <main>
          <Hero />
          <Features />
          <HowItWorks />
          <Integrations />
          <Pricing />
          <Deploy />
          <Contact onSubmit={handleContactSubmit} />
        </main>
        <Footer />
      </div>
    </>
  );
}

export default App;
