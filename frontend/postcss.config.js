import purgecss from '@fullhuman/postcss-purgecss'

const isProd = process.env.NODE_ENV === 'production'

export default {
  plugins: [
    isProd && purgecss({
      content: [
        '../templates/**/*.html',
        './src/**/*.js',
      ],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
      safelist: {
        // Bootstrap JS-toggled classes
        standard: [
          'show', 'showing', 'hiding', 'collapsing', 'fade',
          'active', 'disabled', 'in', 'open',
          'modal-open', 'was-validated',
        ],
        // Selectors containing these patterns (added by Bootstrap JS)
        greedy: [
          /modal/,
          /offcanvas/,
          /dropdown/,
          /tooltip/,
          /popover/,
          /toast/,
          /carousel/,
          /accordion/,
          /collapse/,
          /is-valid/,
          /is-invalid/,
          /tab-pane/,
          /nav-link/,
        ],
      },
    }),
  ].filter(Boolean),
}
