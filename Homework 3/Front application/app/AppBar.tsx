"use client";
import Link from "next/link";
import React from "react";
import styles from '../styles/page.module.css';



const AppBar = () => {

  let token = null;
  if (typeof document !== 'undefined') {
  if(!document?.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1]){

  
    const urlParams = new URLSearchParams(window.location.hash.substring(1));
    let token = urlParams.get('id_token');

    if(token) {
      document.cookie = `token=${token}`;

      window.location.href = 'https://main.d3lbo3t3bvpqcr.amplifyapp.com';
    }
  }else{
    token = document?.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
  }
}
  function signOut() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;"

    window.location.href = 'https://main.d3lbo3t3bvpqcr.amplifyapp.com';
  }

    

  return (
    <div className={styles.description}>
      <div>
        <a
          href="#"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.logo1}
        >
          By a PCD team
        </a>
        <nav className={styles.nav_items}>
          <Link href={"#"}>
            Home
          </Link>
          {token ? (
              <Link href="https://main.d3lbo3t3bvpqcr.amplifyapp.com" onClick={signOut}>Sign out</Link>
            ) : (
              <Link href="https://bankingpcd.auth.eu-central-1.amazoncognito.com/login?response_type=token&client_id=7adrrtamr7vhsc37ehd02aikfe&redirect_uri=https://main.d3lbo3t3bvpqcr.amplifyapp.com">Sign in</Link>
          )}
          <Link href="#">Contact</Link>
        </nav>
      </div>
    </div>

  );
};

export default AppBar;
