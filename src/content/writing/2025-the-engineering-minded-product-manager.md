---
title: The Engineering-Minded Product Manager
date: '2025-11-28'
source: medium
canonical_url: https://medium.com/@ryado/the-engineering-minded-product-manager-80f974dc8801
coauthors: []
tags:
- startup
- software-development
- software-engineering
- product-management
- technology
summary: 'The product-manager counterpart to the product-minded engineer: eight traits of a PM who meets engineering halfway, from technical curiosity to shared ownership of the product.'
reading_time: 7
content_hash: 15ac25c2bef861c8
---

No, the title isn’t a spelling mistake. I swapped the words on purpose.

When I transitioned to product management after years in professional services and engineering-related jobs, I needed to learn on the job, so I started reading about the relationship between engineering and product, looking for what recipes work and what don’t, and how the most successful organizations manage to succeed at building delightful products that push the limits.

<figure>
  <img src="/writing/the-engineering-minded-product-manager/0-l42nK_6cOewbapap.jpg" alt="" loading="lazy" />
  <figcaption>A sailing regatta — Source Wikipedia</figcaption>
</figure>

That’s when I stumbled upon the concept of the “Product-Minded Software Engineer”, by reading an [article](https://blog.pragmaticengineer.com/the-product-minded-engineer/) from Gergely Orosz in the excellent Pragmatic Engineer newsletter. Back then (mid-2022), I had been assigned the integrations ecosystem of ClickHouse as a scope to manage, with thousands of existing integration packages and new ones to build. I was on the lookout for ways to scale our operations while keeping the delivery lean (ClickHouse didn’t yet have a commercial offering until December 2022). So the concept of the product-minded engineer seemed like a viable approach to me.

In short, the idea is to blur the boundaries between product and engineering and expect engineers to take some ownership of product decisions (that’s an oversimplification, but it captures the gist of it).

> “Product-minded engineers are developers with lots of interest in the product itself. They want to understand why decisions are made, how people use the product, and love to be involved in making product decisions”.
> from [the Pragmatic Engineer](https://blog.pragmaticengineer.com/the-product-minded-engineer/)

Our attempt at organizing the integrations ecosystem of a successful and widely adopted database like ClickHouse meant that we had to distribute the ownership of the integrations across product and engineering. With many of these packages being on the critical path of adoption (who cares about the fastest database in the world if the language client can’t keep up?).

The article cited above (which builds upon a [previous one](https://sherifmansour.medium.com/product-engineers-f424da766871) from 2018, by Sherif Mansour) describes the characteristics of a product-minded engineer and what to look for in the engineering profile. Examples include: Proactivity with product ideas and opinions, interest in the business, quick product validation cycles, and 5 to 6 more guiding principles. I highly recommend reading the [article](https://blog.pragmaticengineer.com/the-product-minded-engineer/) cited above to get a grasp of the idea. Writing this post, I also learned that there is a new [O’Reilly book](https://www.oreilly.com/library/view/the-product-minded-engineer/9781098173722/) by Drew Hoskins that discusses this very same topic (I haven’t read it yet, but I plan to do so).

<figure>
  <img src="/writing/the-engineering-minded-product-manager/0-AWM6-TnBDz88kOTu.png" alt="" loading="lazy" />
  <figcaption>Cover of “The Product-Minded Engineer” book by Drew Hoskins, Nov 2025</figcaption>
</figure>

So we got started as a lean team with a sizable scope and bold targets (like any startup team, I guess). My plan was mainly to brief the engineers and raise awareness about this approach, more as a methodology of “working together”, or as the “Product/Engineering contract” if you will.

However, something felt off…

In simple terms, it felt weird to be setting so many expectations for my engineering partners upfront. Talking about the “8 to 10 characteristics of a product-minded engineer” to an engineer colleague was to me the equivalent of writing a letter to Santa, aka asking for all sorts of gifts and treats, because, of course, you have been behaving well during the year. It was a negotiation, and I didn’t have much to trade.

I read somewhere that a successful negotiation isn’t one where you get everything you want, but one where both parties feel like they got a good deal out of it. Building upon this principle, I felt like there’s room for the product manager counterpart of the product-minded engineer, which can “meet the engineers halfway” and turn it into a true partnership.

Let’s swap some words and call it the **Engineering-Minded Product Manager.**

### The Engineering-minded Product Manager

The engineering-minded PM is a product person with a significant interest and some basic skills and knowledge in the engineering craft. They can understand the technical challenges and boundaries of specific products, technology stacks, or features, are aware of the best practices and limitations, and can get into the weeds if needed. They can’t replace software architects, tech leads, or developers, but can hold a productive conversation with them about what’s possible to build, how, and when, and are sensitive to scale and delivery constraints. Finally, they can funnel the engineering feedback and recommendations back into the product requirements, help scope and phase out deliverables, while maintaining a healthy feedback loop with engineering and design partners.

So what are the key aspects of an engineering-minded product manager? While I could see some obvious ones, it was a bit of a tricky question to answer. So I asked my engineering friends and colleagues over time and compiled the following list:

### 1. Technical knowledge: curiosity about the “How”

I might be biased here because I work on fairly technical topics, but I believe that a PM should display some technical curiosity and, if asked, can explain “how the sausage is made” in simple terms. This ensures that the product requirements are grounded in realistic expectations and are a good fit for the phase and maturity stage of the product being built.

### 2. Understanding the technical implications of product decisions

This one ties a bit into the previous point, but in simple terms, it just means that features and the priorities associated with, cannot be decoupled from their technical implications in the software and infrastructure stack. This is especially important when you are chasing “quick wins” that often hide a more complex technical picture.

### 3. Consolidating the user and market signals

While there’s undeniable value in connecting end users and design partners to engineers directly (it’s actually one of the principles of product-minded engineering), user feedback and signals can be overwhelming, ill-formed, or presented with an exaggerated sense of urgency. It’s the role of the product manager to channel it efficiently and combine it with macro-signals from the market and the industry, then translate it into actionable feedback.

### 4. Distilling the product vision, beyond the next feature

In any decent solution, no functionality is ever built in a void, and there’s (or there should be) always a broader plan. This broader plan needs to make sense, obviously, and this “sense” needs to be shared by everyone involved in the project. If, for some reason, the project is taking a “side quest” or we are making a “strategic bet”, the risks associated also need to be shared and understood within the product and engineering teams.

### 5. Getting involved in key engineering decision-making

A product manager can’t make strategic engineering decisions, and shouldn’t. But there’s value in tackling the hard decisions collectively, in a partnership, understanding the implications of key architectural decisions and registering them into the broader vision of the roadmap. A bad architectural choice, for example, can “lock” a project’s ability to evolve beyond the tactical horizon, which ties back into the previous item.

### 6. Constantly on the watch for synergies

A product roadmap is a form of a combinatorial optimization problem. You set milestones and intermediary deliverables, targets and functional areas, and then group the features in sequences that make sense, respect dependencies, and cross-functional constraints. In this exercise, it’s important to be constantly on the watch for “shortcuts” when it makes sense, but also “long paths” and compound effects elsewhere, connecting the dots when possible and building on top of what was built before when possible. It’s a bit like a shortest-path algorithm where you are optimizing not just for velocity, but also for value.

### 7. Technical debt awareness

Moving fast means building technical debt, and every product lives with some of it; there’s no escape from this paradigm. Since there’s no escape, it’s important to acknowledge the technical debt when it reaches a certain level and address it/budget for it. I think of it as a healthy cycle where you sprint to a useful version of a product to prove value, then halt and consolidate, before restarting.

### 8. Shared-ownership of the product

The product function doesn’t stop when the feature is shipped; it actually accelerates. It’s everyone’s responsibility to make it a success, and there’s no such thing as “last handover to engineering” in practice. If a user faces an issue, raises a ticket, or triggers an escalation, it’s pretty much all hands on deck, and product should not be excluded. The feedback collected in these situations is actually invaluable.

### Closing remarks

A lot of what I wrote above might feel like common sense, and in fact, it is a form of common sense, but I believe that it’s important to be intentional about it, as it’s the basis of the product/engineering contract.

Product-minded engineering is a great tool, but not a magical solution to all scaling and delivery challenges. It requires care and attention to implement and a product organization that can adapt, compromise, and meet the engineering function in the middle. That’s why I believe that to succeed, an engineering-minded PM counterpart is not just “fair”, but necessary.

**Thank you**
Huge thanks to my colleagues and friends at ClickHouse (Integrations, ClickPipes, AI/ML, and elsewhere) who spent time with me in the trenches and also helped me brainstorm these ideas.
