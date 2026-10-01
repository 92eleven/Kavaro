import { useState, useEffect } from 'react';

export function LoadAnimation({ onComplete }: { onComplete: () => void }) {
  const [phase, setPhase] = useState<'letters' | 'flicker' | 'glow' | 'fadeout'>('letters');
  const [visibleLetters, setVisibleLetters] = useState<number[]>([]);

  useEffect(() => {
    const letters = ['A', 'V', 'A', 'R', 'O'];
    let currentIndex = 0;

    const letterInterval = setInterval(() => {
      if (currentIndex < letters.length) {
        setVisibleLetters(prev => [...prev, currentIndex]);
        currentIndex++;
      } else {
        clearInterval(letterInterval);
        setTimeout(() => setPhase('flicker'), 300);
      }
    }, 120);

    return () => clearInterval(letterInterval);
  }, []);

  useEffect(() => {
    if (phase === 'flicker') {
      let flickerCount = 0;
      const flickerInterval = setInterval(() => {
        flickerCount++;
        if (flickerCount >= 6) {
          clearInterval(flickerInterval);
          setPhase('glow');
        }
      }, 100);
      return () => clearInterval(flickerInterval);
    }
  }, [phase]);

  useEffect(() => {
    if (phase === 'glow') {
      const timer = setTimeout(() => {
        setPhase('fadeout');
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [phase]);

  useEffect(() => {
    if (phase === 'fadeout') {
      const timer = setTimeout(() => {
        onComplete();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [phase, onComplete]);

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center transition-opacity duration-500 ${
        phase === 'fadeout' ? 'opacity-0' : 'opacity-100'
      }`}
      style={{ backgroundColor: '#0F0F1A' }}
    >
      <div className="flex items-center">
        <span
          className={`font-exo font-black text-6xl md:text-8xl lg:text-9xl transition-all duration-100 ${
            phase === 'flicker' && Math.floor(Date.now() / 100) % 2 === 0 ? 'opacity-30' : ''
          }`}
          style={{
            color: '#00C9E8',
            transform: 'skewX(-22deg)',
            textShadow:
              phase === 'glow' || phase === 'fadeout'
                ? '0 0 12px #00C9E8, 0 0 24px rgba(0, 201, 232, 0.6)'
                : 'none',
            animation: phase === 'glow' ? 'pulse-glow 2s ease-in-out infinite' : 'none',
          }}
        >
          K
        </span>
        <span
          className={`font-exo font-black text-6xl md:text-8xl lg:text-9xl transition-all duration-500 ${
            visibleLetters.length > 0 ? 'opacity-100' : 'opacity-0'
          }`}
          style={{
            color: '#6B7280',
            transform: 'skewX(-22deg)',
            display: 'inline-block',
          }}
        >
          AVARO
        </span>
      </div>
    </div>
  );
}
