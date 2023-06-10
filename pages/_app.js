import Layout from "@/components/layout/layout";
import "@/styles/globals.css";
import { useRouter } from "next/router";
import "bootstrap/dist/css/bootstrap.css";
import { motion, AnimatePresence } from "framer-motion";
import { useEffect } from "react";
import Footer from "@/components/layout/footer";
export default function App({ Component, pageProps }) {
  const router = useRouter();
  useEffect(() => {
    require("bootstrap/dist/js/bootstrap.bundle");
  }, []);
  return (
    <Layout>
      <motion.div
        key={router.route}
        initial="initial"
        animate="animate"
        variants={{
          initial: {
            opacity: 0,
          },
          animate: {
            opacity: 1,
          },
        }}
      >
        <Component {...pageProps} />
      </motion.div>
      <div style={{ marginTop: "268px" }}>
        <Footer></Footer>
      </div>
    </Layout>
  );
}
