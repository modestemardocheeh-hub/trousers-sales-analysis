# Partie 1 : Chargement et préparartion 
# 1. Chargement de fichier 
import pandas as pd 
df=pd.read_csv("trouver_date.csv")
# 2. Nettoyage de colone
df["Price"]=df["Price"].str.replace("$","",regex=False).astype(float) 
# 3. Conversion en datetime
df["Date"]=pd.to_datetime(df["Date"])
# 4,5 & 6 . Création de colone 
df["Mois"]=df["Date"].dt.month
df["Semaine"]=df["Date"].dt.isocalendar().week 
df["Jour"]=df["Date"].dt.day
df["Nom_mois"]=df["Mois"].apply(lambda x : "Aout" if x==8 else "September" if x==9 else "October" if x==10 else "Le mois n'existe pas")
df["Gamme"]=df["Price"].apply(lambda x : "Luxe" if x>120 else "Standard" if x>80 else "Economique")
df["CA_commande"]=df.groupby("Order Number")["Price"].sum()
# Résumé complet sur le fichier
print(f"Le nombre de ligne est : {df.shape[0]} et le nombre de colone est : {df.shape[1]} \n")
print("Les colones existantes sont : ",df.columns)
print(" \n Le type des colones sont décrit tels que : \n",df.dtypes)
print(" Pour plus d'info consultez ce petit recap suivant : \n",df.describe())
# Parie 2 : Statistiques descriptives
# 8. Calcul sur les prix
print("Le prix moyen,médian,minimum,maximum et l'ecart type des prix de service de cet entreprise sont : \n",df["Price"].agg(Prix_Moyen="mean",Prix_médian="median",Prix_minimial="min",Prix_maximal="max",Ecart_type_prix="std"))
# 9. Calcul sur les prix
A=df["Order Number"].value_counts()
print(f"Le nombre de comandes uniques est : {len(A[A.values==1])}")
# 10. Répartition des ventes par gamme en pourcentages
print(f"\n Par gamme la répartition des ventes donne : {df["Gamme"].value_counts(normalize=True)*100}")
# 11. Top 5 produits les plus vendus
print("\n Le top 5 des produit les plus vendus donne : \n",df["Product"].value_counts().sort_values(ascending=False).head(5))
# 12. Top 5 produit les plus rentables 
print("\n Le Top 5 des produits les plus rentables donne : \n",df.groupby("Product")["Price"].sum().sort_values(ascending=False).head(5))
# Partie 3 : Analyse des paiements 
# 13. Nombre de ventes et chiffre affaire par pMéthode de payement
print("Le nombre de ventes par paiement donne : \n",df["Payment Method"].value_counts())
print("Le chiffre d'affaire par payement donne : \n",df.groupby("Payment Method")["Price"].sum())
# 14. Pourcentage de chaque Méthode de payement 
print(f"Le pourcentage d'utilisation par méthode de payement donne : \n{df["Payment Method"].value_counts(normalize=True)*100} \n")
# 15. Méthode de paiement préférée pour chaque gamme de produit
ts_g_mme=set(df["Gamme"].values)
for g_mme in ts_g_mme :
    B=df.groupby("Gamme")["Payment Method"].value_counts().sort_values(ascending=False).reset_index()
    B=B[B["Gamme"]==g_mme]["Payment Method"].values
    print(f"Pour la gamme {g_mme} la méthode de paiement préférée est : {B[0]}")
# Partie 4 : Analyse Temporelle
# 16. CA par jour 
print("Le chiffre d'affaire par jour donne : \n",df.groupby("Jour")["Price"].sum())
print("\n Le meilleur jour est : ",df.groupby("Jour")["Price"].sum().idxmax())
print("\n Le pire jour est b: ",df.groupby("Jour")["Price"] .sum().idxmin())
# 17. CA par semaine
print(" Le CA par semaine nous donne : \n",df.groupby("Semaine")["Price"])
# 18. CA par mois
print("Le chiffre d'affaire par mois donne : \n",df.groupby("Mois")["Price"])
# 19. Nombre de ventes par jour de la semaine 
df["Jour_Semaine"]=df["Date"].dt.dayofweek
print(" Le nombre de ventes par jour donne : \n",df.groupby("Jour_Semaine")["Price"].size())
# 20. Mois le plus actif et le moins actif
print("Le mois le plus actif est le ",df[df["Mois"]==df["Mois"].value_counts().idxmax()]["Nom_mois"].values[0])
print(" Le mois le moins actif est ",df[df["Mois"]==df["Mois"].value_counts().idxmin()]["Nom_mois"].values[0])
# Partie 5 : Analyse des commandes 
# 21. Nombre moyens d'article 
print("Le nombre moyen d'article par commande est : ",df["Order Number"].value_counts().mean())
# 22. Top 10 commandes les plus chères 
print("Le Top 10 des commandes les plus chères donne : \n",df.groupby("Order Number")["Price"].sum().sort_values(ascending=False).head(10))
# 23. Nombre de commandes avec plusieurs articles
print(" Les commandes à plusieurs valeurs articles sont les numéros qui suivent : \n",list(A[A.values>=2].index))
# 24. CAmoyen par commande
print("Le chiffre moyen par commande est : ",df.groupby("Order Number")["Price"].mean())
# Partie 6. Tableau croisé dynamique
# 25 Pivot table de produit,méthode de paiementet nombre de ventes
print(pd.pivot_table(df,index="Product",values="Price",columns="Payment Method",aggfunc="count",fill_value=0))
# 26. Pivot table de mois,gamme et prix d'affaire
print(pd.pivot_table(df,index="Mois",values="Price",columns="Gamme",aggfunc="sum",fill_value=0))
# 27. Distribution des prix
import matplotlib.pyplot as plt 
plt.hist(df["Price"],bins=15,color="red",edgecolor="black")
plt.title(" Distribuion des prix",fontsize=16,fontweight="bold")
plt.xlabel("Prix en dollar",fontsize=12)
plt.ylabel(" Nombre de ventes ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 28. Top 10 produit 
produit_top_10=df.groupby("Product")["Price"].sum().sort_values(ascending=False).head(10)
plt.barh(produit_top_10.index,produit_top_10 .values,color="yellow",edgecolor="green")
plt.title(" Top 10 des produits selon leur chiffre affaires ",fontsize=16,fontweight="bold")
plt.xlabel(" Produit ",fontsize=12)
plt.ylabel(" Prix d'affaire ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 29. Répartiton des méthode de paiements
nbre_ventes_mth_payment=df["Payment Method"].value_counts().sort_index()
plt.pie(nbre_ventes_mth_payment.values,labels=nbre_ventes_mth_payment.index,colors=["green","red","blue","orange"],autopct="%1.1f%%",startangle=90,explode=(0.05,0.05,0.05,0.05))
plt.title("Répartition des méthodes de paiements",fontsize=16,fontweight="bold")
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 30. Evolution de chiffre d'affaire
CA_jour=df.groupby("Jour")["Price"].sum()
plt.plot(CA_jour.index,CA_jour.values,color="red",linewidth=2,marker="o")
plt.title(" Evolution de chiffre affaire par jour ",fontsize=16,fontweight="bold")
plt.xlabel(" Jour ",fontsize=12)
plt.ylabel(" Chiffre d'affaire ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 31 . CA par mois
CA_mois=df.groupby("Mois")["Price"].sum()
plt.bar(CA_mois.index,CA_mois.values,color="black",edgecolor="red")
plt.title(" Chiffre d'affaire par mois ",fontsize=16,fontweight="bold")
plt.xlabel(" Mois",fontsize=12)
plt.ylabel(" Chiffre affaire ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 32. CA 
plt.figure(figsize=(14,10))
plt.subplot(2,2,1)
CA_gamme=df.groupby("Gamme")["Price"].sum()
plt.plot(CA_gamme.index,CA_gamme.values,color="yellow",linewidth=2,marker="s")
plt.title(" Prix par gamme ",fontsize=16,fontweight="bold")
plt.xlabel("Gamme",fontsize=12)
plt.ylabel(" Chiffre affaire ",fontsize=12)
plt.tight_layout()
plt.subplot(2,2,2)
V_gamme=df["Gamme"].value_counts().sort_index()
plt.plot(V_gamme.index,V_gamme.values,color="blue",linewidth=2,marker="D")
plt.title(" Ventes par gamme ",fontsize=16,fontweight="bold")
plt.xlabel("Gamme",fontsize=12)
plt.ylabel(" Nombre de ventes ",fontsize=12)
plt.tight_layout()
plt.subplot(2,2,3)
CA_méhode=df.groupby("Payment Method")["Price"].sum()
plt.plot(CA_méhode.index,CA_méhode.values,color="yellow",linewidth=2,marker="s")
plt.title(" Prix par méthode ",fontsize=16,fontweight="bold")
plt.xlabel("Méthode",fontsize=12)
plt.ylabel(" Chiffre affaire ",fontsize=12)
plt.tight_layout()
plt.subplot(2,2,4)
V_méthode=df["Payment Method"].value_counts().sort_index()
plt.plot(V_méthode.index,V_méthode.values,color="black",linewidth=2,marker="D")
plt.title(" Ventes par méthode ",fontsize=16,fontweight="bold")
plt.xlabel("Méthode",fontsize=12)
plt.ylabel(" Nombre de ventes ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 33. Evolution des ventes par jour de la semaine
V_j_semaine=df["Jour_Semaine"].value_counts().sort_index()
plt.plot(V_j_semaine.index,V_j_semaine.values,color="red",linewidth=2,marker="D")
plt.title(" Ventes par jour de la semaine ",fontsize=16,fontweight="bold")
plt.xlabel("Jour de la semaine",fontsize=12)
plt.ylabel(" Nombre de ventes ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# 34. Distribution des CA par commmande
CA_commande=df.groupby("Order Number")["Price"].sum()
plt.hist(CA_commande.values,bins=15,color="red",edgecolor="black")
plt.title(" Distribuion des prix",fontsize=16,fontweight="bold")
plt.xlabel("Prix en dollar",fontsize=12)
plt.ylabel(" Nombre de ventes par Order Number ",fontsize=12)
plt.tight_layout()
plt.show(block=False)
plt.pause(20)
plt.close()
# Partie 8
# 35. Rapport 
with pd.ExcelWriter("rapport_trouvers2.xlsx", engine="xlsxwriter") as writer :
   df.to_excel(writer,sheet_name="Feuille_1",index=False)
   df.groupby("Product")["Price"].sum().to_excel(writer,sheet_name="Feuille_2")
   df.groupby("Payment Method")["Price"].sum().to_excel(writer,sheet_name="Feuille_3")
   df.groupby("Mois")["Price"].sum().to_excel(writer,sheet_name="Feuille_4")
   p_v=pd.pivot_table(df,index="Product",values="Price",columns="Payment Method",aggfunc="count",fill_value=0)
   p_v.to_excel(writer,sheet_name="Feuille_5")