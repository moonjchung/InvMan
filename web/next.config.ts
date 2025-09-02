import type { NextConfig } from "next";

// @ts-check

/**
 * @type {import('@sentry/nextjs').SentryBuildOptions}
 */
const sentryBuildOptions = {
  // For all available options, see:
  // https://github.com/getsentry/sentry-webpack-plugin#options

  // Suppresses source map uploading logs during build
  silent: true,
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  // An auth token is required for uploading source maps.
  authToken: process.env.SENTRY_AUTH_TOKEN,
};

/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  // Your existing configuration
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/:path*",
      },
    ];
  },
  sentry: {
    // For all available options, see:
    // https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/

    // Upload a larger set of source maps for prettier stack traces (increases build time)
    widenClientFileUpload: true,

    // Hides source maps from generated client bundles
    hideSourceMaps: true,

    // Automatically tree-shake Sentry logger statements to reduce bundle size
    disableLogger: true,

    // Enables automatic instrumentation of Vercel Cron Monitors. (Does not yet work with App Router.)
    // See the following for more information:
    // https://docs.sentry.io/platforms/javascript/guides/nextjs/cron/
    // https://vercel.com/docs/cron-jobs
    automaticVercelMonitors: true,
  },
};

// Make sure to source this file in Sentry.config.js
const { withSentryConfig } = require("@sentry/nextjs");

module.exports = withSentryConfig(nextConfig, sentryBuildOptions);
