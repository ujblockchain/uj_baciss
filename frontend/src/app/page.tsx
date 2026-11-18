import { SignedInRedirect } from "@/features/auth/components/signed-in-redirect";

/** The root address only decides where to go: login, or the role's home. */
const Home = () => {
  return <SignedInRedirect />;
};

export default Home;
