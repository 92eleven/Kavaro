import { Mail, MessageSquare, Calendar, Plug } from 'lucide-react';

const integrations = [
  {
    icon: Mail,
    title: 'Gmail / Email',
    description: 'Monitors inbox, responds naturally, sends confirmations and follow-ups automatically',
  },
  {
    icon: MessageSquare,
    title: 'Twilio SMS',
    description: 'Qualifies leads via text, sends reminders and follow-up messages',
  },
  {
    icon: Calendar,
    title: 'Google Calendar',
    description: 'Checks availability, books appointments, sends calendar invites automatically',
  },
  {
    icon: Plug,
    title: 'Webhook / REST API',
    description: 'Connect any system via REST API. POST a lead and Kavaro handles the rest in real time',
  },
];

export function Integrations() {
  return (
    <section id="integrations" className="py-20 md:py-32 bg-surface">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-exo font-black text-3xl md:text-4xl lg:text-5xl text-text">
            Meets Leads Where They Are.
          </h2>
          <p className="mt-4 text-lg md:text-xl text-primary/70">
            Email. SMS. Web. Calendar.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 md:gap-8">
          {integrations.map((integration, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center">
                  <integration.icon className="w-7 h-7 text-accent" />
                </div>
                <div>
                  <h3 className="font-exo font-bold text-xl text-text mb-2">{integration.title}</h3>
                  <p className="text-primary/70 leading-relaxed">{integration.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-primary rounded-2xl p-6 md:p-8 text-center">
          <p className="text-white/90 text-lg">
            <span className="text-accent font-semibold">Channel-agnostic architecture.</span> Add new channels without touching the core qualification engine.
          </p>
        </div>
      </div>
    </section>
  );
}
