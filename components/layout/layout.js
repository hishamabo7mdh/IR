import { Fragment } from "react";

import Link from "next/link";
function Layout(props) {
  return (
    <Fragment>
      <main
        style={{
          backgroundImage: `url("/images/bg3.jpg")`,
          height: "100%",
          backgroundRepeat: "repeat-x",
          backgroundAttachment: "fixed",
          backgroundSize: "cover",
        }}
      >
        {props.children}
      </main>
    </Fragment>
  );
}
export default Layout;
