"use client";

import React from "react";
import Image from 'next/image'
import styles from '../styles/page.module.css'




const HomePage = () => {

  let token =false;
  if (typeof document !== 'undefined') {
    // Your code that uses the document object here
    if(document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1]) {
      token = true;
    }
  }

  return (
    <main className={styles.main}>
      {token ? (
<>
      <div className={styles.square_card}>
				<div className={styles.balance}>
					<h4>Balance: $100.00</h4>
				</div>
        <button >ADD</button>
        <button >WITHDRAW</button>
				<ul className={styles.transaction}>
					<li>
						<span className={styles.transaction_date}>March 31, 2023</span>
						<span className={styles.transaction_amount}>$20.00</span>
					</li>
					<li>
						<span className={styles.transaction_date}>March 30, 2023</span>
						<span className={styles.transaction_amount}>$50.00</span>
					</li>
					<li>
						<span className={styles.transaction_date}>March 29, 2023</span>
						<span className={styles.transaction_amount}>$30.00</span>
					</li>
				</ul>
			</div>
</>
            ) : (
      <>
      <div className={styles.center}>
        <Image
          className={styles.logo}
          src="/home.jpg"
          alt="Home Logo"
          width={400}
          height={250}
          priority
        />
      </div>

      <div className={styles.grid}>
        <a
          href=""
          className={styles.card}
          

        >
          <h2 >
            Projects <span>-&gt;</span>
          </h2>
          <p >
            Making people successfull in a changing word.
          </p>
        </a>

        <a
          href=""
          className={styles.card}
          

        >
          <h2 >
            Skills <span>-&gt;</span>
          </h2>
          <p >The best you can get.</p>
        </a>

        <a
          href=""
          className={styles.card}
          

        >
          <h2 >
            Network <span>-&gt;</span>
          </h2>
          <p >
            The home of banking.
          </p>
        </a>
      </div>
      </>
       )}
    </main>
  )
};

export default HomePage;
