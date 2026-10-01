import { Check } from 'lucide-react';

const plans = [
  {
    name: 'Starter',
    price: '$297',
    period: '/month',
    setupFee: '+ $497 one-time setup fee',
    features: [
      'Single channel (web or email)',
      'Standard qualification criteria',
      'Google Calendar integration',
      'Basic analytics dashboard',
      'Up to 500 leads/month',
    ],
    highlighted: false,
  },
  {
    name: 'Growth',
    price: '$497',
    period: '/month',
    setupFee: '+ $997 one-time setup fee',
    features: [
      'Multi-channel (web + email + SMS)',
      'Custom scoring logic',
      'CRM integration (HubSpot/GoHighLevel)',
      'Full audit trail + self-improving loop',
      'Up to 2,000 leads/month',
    ],
    highlighted: true,
    badge: 'Most Popular',
  },
  {
    name: 'Scale',
    price: '$997',
    period: '/month',
    setupFee: '+ $1,997 one-time setup fee',
    features: [
      'Everything in Growth',
      'White-label ready',
      'Custom integrations',
      'Priority support',
      'Unlimited leads',
      'Dedicated onboarding',
    ],
    highlighted: false,
  },
];

export function Pricing() {
  const scrollToContact = () => {
    const element = document.querySelector('#contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="pricing" className="py-20 md:py-32 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-exo font-black text-3xl md:text-4xl lg:text-5xl text-text">
            Simple, Transparent Pricing.
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`rounded-2xl p-8 ${
                plan.highlighted
                  ? 'bg-white border-2 border-accent shadow-lg relative'
                  : 'bg-white border border-gray-200'
              }`}
            >
              {plan.badge && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-accent text-primary text-sm font-bold px-4 py-1 rounded-full">
                    {plan.badge}
                  </span>
                </div>
              )}

              <h3 className="font-exo font-bold text-2xl text-text mb-4">{plan.name}</h3>
              <div className="mb-6">
                <span className="font-exo font-black text-4xl text-text">{plan.price}</span>
                <span className="text-primary/60 ml-1">{plan.period}</span>
              </div>
              <p className="text-sm text-gray-400 -mt-4 mb-6">{plan.setupFee}</p>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
                    <span className="text-primary/70">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={scrollToContact}
                className={`w-full py-3 rounded-xl font-semibold transition-all ${
                  plan.highlighted
                    ? 'bg-accent text-primary hover:bg-accent/90 shadow-md hover:shadow-lg'
                    : 'bg-surface text-primary hover:bg-primary/10'
                }`}
              >
                Get Started
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
