**Description**

The data is related with direct marketing campaigns of a banking institution. The marketing campaigns were based on phone calls. Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be ('yes') or not ('no') subscribed.

**Input variables:**

1 last contact date: last contact date

2 age (numeric)

3 job : type of job

4 marital : marital status (categorical: "married","divorced","single"; note: "divorced" means divorced or widowed)

5 education (categorical: "unknown","secondary","primary","tertiary")

6 default: has credit in default? (binary: "yes","no")

7 balance: average yearly balance, in euros (numeric)

8 housing: has housing loan? (binary: "yes","no")

9 loan: has personal loan? (binary: "yes","no")

10 contact: contact communication type (categorical: "unknown","telephone","cellular")

11 duration: last contact duration, in seconds (numeric)

12 campaign: number of contacts performed during this campaign and for this client (numeric, includes last contact)

13 pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric, -1 means client was not previously contacted)

14 previous: number of contacts performed before this campaign and for this client (numeric)

15 poutcome: outcome of the previous marketing campaign (categorical: "unknown","other","failure","success")

**Output variable (desired target):**

16 target: has the client subscribed a term deposit? (binary: "yes","no")


