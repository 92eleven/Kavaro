import { Brain, CalendarCheck, Target, BarChart3 } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Qualification',
    description: 'Kavaro engages every lead in a natural conversation, asking the right questions to determine fit. Uses OpenAI GPT-4o with your custom qualification criteria.',
  },
  {
    icon: CalendarCheck,
    title: 'Automatic Booking',
    description: 'Qualified leads are immediately offered a time slot. Kavaro checks availability, books the appointment, and sends a confirmation — all in one interaction.',
  },
  {
    icon: Target,
    title: 'Custom Criteria',
    description: 'You define what "qualified" means — budget, company size, decision-maker status. Kavaro scores every lead against your exact requirements.',
  },
  {
    icon: BarChart3,
    title: 'Performance Analytics',
    description: 'See qualification rates, booked appointments per week, and conversion analytics. Know exactly how your pipeline is performing.',
  },
];

export function Features() {
  return (
    <section id="features" className="py-20 md:py-32 bg-surface">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-exo font-black text-3xl md:text-4xl lg:text-5xl text-text">
            Everything You Need.<br />Nothing You Don't.
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6 md:gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-accent/10 rounded-xl flex items-center justify-center">
                  <feature.icon className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <h3 className="font-exo font-bold text-xl text-text mb-2">{feature.title}</h3>
                  <p className="text-primary/70 leading-relaxed">{feature.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-accent/5 border border-accent/20 rounded-2xl p-6 md:p-8 text-center">
          <p className="text-primary/80 text-lg md:text-xl">
            Businesses using Kavaro typically see a <span className="font-bold text-accent">40-60% reduction</span> in time spent on lead screening and a <span className="font-bold text-accent">measurable increase</span> in booked appointments.
          </p>
        </div>
      </div>
    </section>
  );
}
