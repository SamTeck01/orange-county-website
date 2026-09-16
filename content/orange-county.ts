export const positioning = {
  tagline: "...not for everyone.",
  body: "Orange County is an avant-garde residential estate that represents the height of modern living and a prime investment opportunity in Balogun, Oyo, Nigeria. Developed by Pace consult.",
};

export const documentation = {
  items: ["Allocation Letter", "Deed of Agreement", "Receipt"],
};

export const landTitle = {
  items: ["C of O in View", "Registered Survey Plan"],
};

export const features = [
  { n: "01", title: "Good Road Network",
    body: "Experience hassle-free mobility within the estate, thanks to strategically planned and well-maintained road infrastructure that guarantees smooth and convenient access." },
  { n: "02", title: "Solar Street Light",
    body: "Experience the perfect harmony of safety and style with solar-powered street lights, illuminating your estate with elegance." },
  { n: "03", title: "CCTV Camera",
    body: "Security without compromise. With full-time CCTV monitoring, your estate remains protected day and night." },
  { n: "04", title: "Gated Community",
    body: "Embrace the comfort and elegance of a private gated community, where every moment reflects tranquility and refined living." },
];

export const location = {
  area: "Balogun, Oyo.",
  road: "Off Iseyin Express",
  coordinates: null,   // no GPS in the brief — render the map moment without a pin
};

export const landmarks = [
  { title: "Off Iseyin Express",
    body: "Strategically located along Off Iseyin Express, just minutes from OrangeCounty — putting you close to growth, connectivity, and everyday essentials." },
  { title: "Div Police HQ, Balogun",
    body: "In close proximity to the Divisional Police Headquarters, offering added security and easy accessibility." },
  { title: "Africhatta film village",
    body: "Just 2-3 Minutes from Afri Chatta Film Village — strategically positioned close to a major entertainment and tourism destination with growing activity and development." },
  { title: "Danbaba Asphalt plant",
    body: "Just 2 Minute to the Orange County — strategically located close to a major industrial landmark, offering excellent accessibility and proximity to growing commercial activity." },
];

// Facilities genuinely have NO descriptions in the brief. body stays null.
// The Facilities section is one of the TWO places cards are allowed — the card must be
// composed to work on image + label alone, not to look like a card missing its text.
export const facilities = [
  { title: "Gym Center",     body: null },
  { title: "Football Pitch", body: null },
  { title: "Basketball Court", body: null },
  { title: "Mini Mart",      body: null },
];

export const benefits = [
  { title: "Secure & Controlled Environment", lead: null, points: [] },
  { title: "Flexible Payment Structure",
    lead: "Structured installment framework allowing:",
    points: ["Entry with manageable commitment", "Phased payments", "Early lock-in advantage"] },
  { title: "Institutional Backing & Professional Oversight",
    lead: "Powered by Pace Associates:",
    points: ["Survey clarity", "Allocation transparency", "Structured documentation", "Professional project supervision"] },
  { title: "Strategic Growth Corridor Advantage",
    lead: "Strategically located in Balogun Oyo — an emerging area with strong growth potential and promising investment advantages.",
    points: [] },
  { title: "Structured & Professionally Managed Estate Layout",
    lead: "Planned with proper:",
    points: ["Road network", "Drainage alignment", "Plot demarcation", "Controlled development guidelines"] },
  { title: "Investment Appreciation Potential",
    lead: "Early-entry pricing within a developing axis positions buyers for:",
    points: ["Medium-term capital gain", "Resale profitability", "Rental development opportunity"] },
];

export const communityVision = {
  lead: "Orange County is not just plots.\nIt is planned to evolve into:",
  points: ["A premium residential cluster", "Organized neighborhood ecosystem", "Long-term livable investment hub"],
};

export const plots = [
  { size: "300sqm",          price: 500000,  display: "₦500,000",   availability: null },
  { size: "450sqm",          price: 750000,  display: "₦750,000",   availability: null },
  { size: "600sqm",          price: 1000000, display: "₦1,000,000", availability: null },
  { size: "Commercial Plots", price: 1000000, display: "₦1,000,000", availability: null },
];

export const payment = {
  accountName: "Orange County by Pace Consult",
  bank: "Zenith Bank",
  accountNumber: "1311968377",
  steps: null,   // no documented purchase steps — render the designed empty state
};

export const contact = {
  email: "Paceconsultltd@gmail.com",
  instagram: "@Paceconsult_associates",
  instagramUrl: "https://instagram.com/Paceconsult_associates",
  phones: ["07034680780", "08173676999", "08168781298"],
  // WhatsApp deep links use the international form of the first number.
  whatsappPrimary: "2347034680780",
  hours: null,
  officeAddress: null,
};

export const developer = { name: "Pace Consult" };

export type Positioning = typeof positioning;
export type Documentation = typeof documentation;
export type LandTitle = typeof landTitle;
export type Feature = (typeof features)[number];
export type Location = typeof location;
export type Landmark = (typeof landmarks)[number];
export type Facility = (typeof facilities)[number];
export type Benefit = (typeof benefits)[number];
export type CommunityVision = typeof communityVision;
export type Plot = (typeof plots)[number];
export type Payment = typeof payment;
export type Contact = typeof contact;
export type Developer = typeof developer;
