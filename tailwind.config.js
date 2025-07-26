// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
    './routes/**/*.py',
    './logic/**/*.py'
  ],
  theme: {
    extend: {},
  },
  safelist: [
    "bg-brand", "btn", "btn:hover", "glass-box", "input", "modal", "modal.active",
    "heading-xl", "paragraph", "slider-container", "text-center", "text-left", "text-right",
    "md:text-4xl", "text-gray-700", "text-cyan-700", "rounded-xl", "rounded-2xl", "rounded-full",
    "shadow", "shadow-lg", "backdrop-blur-md", "border", "border-cyan-100", "font-bold", "font-inter",
    "hover:underline", "focus:ring-2", "focus:outline-none", "px-4", "py-1", "px-6", "py-3",
    "w-full", "w-fit", "w-20", "w-24", "h-20", "h-24", "h-screen", "min-h-screen", "z-10", "z-50",
    "top-0", "left-0", "right-0", "bottom-0", "sticky", "relative", "absolute", "flex", "items-center",
    "justify-between", "justify-center", "mx-auto", "space-x-6", "space-y-4", "gap-2", "text-xl",
    "text-sm", "text-base", "text-2xl", "text-4xl", "leading-relaxed", "md:hidden", "md:flex",
    "hidden", "block", "inline-block", "truncate", "overflow-hidden", "border-gray-300",
    "bg-white", "bg-white/60", "bg-gradient-to-br", "from-[#d8e850]", "to-[#99e3f9]"
  ]
}
