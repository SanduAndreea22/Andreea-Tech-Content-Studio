# Cum lucram: reguli de serviciu

Reguli stabilite de Andreea. Site-ul trebuie sa spuna doar ce se poate sustine. Daca o regula se schimba, se schimba mai intai aici, apoi pe site (`studio/templates/studio/services.html`, `studio/packages.py`).

1. **Plata:** 100% inainte de inceperea lucrului. Dupa ce clientul alege pachetul, Andreea trimite detaliile de plata.
2. **Termene:** 1 Ad, 3 Ads si Starter Posts: 3 zile lucratoare. Growth Pack: 5 zile lucratoare. Full Month: 7 zile lucratoare. Se calculeaza din momentul platii.
3. **Revizii:** 2 runde de modificari, maximum 2 zile lucratoare fiecare.
4. **Brief:** descrierea afacerii, publicul tinta, linkurile sociale si preferintele de brand.
5. **Livrare:** prin email, intr-un document.
6. **Mostra gratuita:** o reclama scurta, trimisa pe email in 2 zile lucratoare, oricui completeaza formularul.
7. **Preturi:** fixe pe pachet, niciodata pe ora.

8. **Date personale:** mesajele din formular se pastreaza maximum 12 luni, apoi se sterg. Pagina Privacy de pe site promite asta. Ruleaza la fiecare 6 luni `python manage.py delete_old_requests` (arata cate mesaje sunt vechi), apoi `python manage.py delete_old_requests --yes` ca sa le stearga. Pune-ti un memento in calendar.
9. **Client tinta:** business-uri care nu stiu cum sa isi faca reclame si postari sau nu au timp.

Formularea din site (engleza): "You pay upfront. Once you select a package, I'll send you the payment details."

Principiu: nu promitem nimic ce nu putem livra.
