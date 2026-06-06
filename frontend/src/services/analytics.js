import ReactGA from "react-ga4";

export const initializeAnalytics = () => {
  const measurementId = import.meta.env.VITE_GA_MEASUREMENT_ID;

  if (measurementId) {
    ReactGA.initialize(measurementId);
  }
};