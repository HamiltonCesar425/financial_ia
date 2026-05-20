import AudienceSection from "../../../components/AudienceSection"
import FeaturesSection from "../../../components/FeaturesSection"
import Footer from "../../../components/Footer"
import HeroSection from "../../../components/HeroSection"
import TransparencySection from "../../../components/TransparencySection"

export default function Home({ onStart }) {
  return (
    <main className="marketing-page">
      <HeroSection onStart={onStart} />
      <FeaturesSection />
      <AudienceSection />
      <TransparencySection />
      <Footer />
    </main>
  )
}
