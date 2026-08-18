import sys
import os
import joblib
import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)


# ============================================================
# 1. CHEMIN DU PROJET
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# 2. CHARGEMENT DU MODELE SLA
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "output",
    "model_sla_rf_tfidf.pkl"
)

model_sla = joblib.load(MODEL_PATH)

print("Modèle SLA chargé avec succès.")


# ============================================================
# 3. FONCTION DE PREDICTION
# ============================================================

def predire_sla():

    # Récupérer les informations saisies
    ticket = pd.DataFrame([{
        "Priorité": priorite.currentText(),
        "Categorie": categorie.currentText(),
        "Titre de la demande": titre_ticket.text()
    }])

    # Vérifier que le titre n'est pas vide
    if titre_ticket.text().strip() == "":
        resultat.setText(
            "Résultat : ⚠ Veuillez saisir le titre du ticket."
        )
        probabilite.setText("Probabilité : --")
        return

    # Faire la prédiction
    prediction = model_sla.predict(ticket)[0]

    # Calculer la probabilité de dépassement
    probabilite_depassement = model_sla.predict_proba(
        ticket
    )[0, 1]

    # Afficher le résultat
    if prediction == 1:

        resultat.setText(
            "Résultat : ⚠ RISQUE DE DÉPASSEMENT SLA"
        )

    else:

        resultat.setText(
            "Résultat : ✓ SLA PROBABLEMENT RESPECTÉ"
        )

    # Afficher la probabilité
    probabilite.setText(
        f"Probabilité de dépassement : "
        f"{probabilite_depassement:.2%}"
    )


# ============================================================
# 4. CREATION DE L'APPLICATION
# ============================================================

app = QApplication(sys.argv)

window = QWidget()

window.setWindowTitle(
    "Helpdesk SLA Predictor"
)

window.resize(600, 500)


# ============================================================
# 5. TITRE DE L'APPLICATION
# ============================================================

titre_app = QLabel(
    "Helpdesk SLA Predictor",
    parent=window
)

titre_app.move(200, 30)


# ============================================================
# 6. PRIORITE
# ============================================================

label_priorite = QLabel(
    "Priorité :",
    parent=window
)

label_priorite.move(50, 100)


priorite = QComboBox(
    parent=window
)

priorite.addItems([
    "Critique (P1)",
    "Élevée (P2)",
    "Moyenne (P3)",
    "Faible (P4)"
])

priorite.move(200, 95)

priorite.resize(
    300,
    30
)


# ============================================================
# 7. CATEGORIE
# ============================================================

label_categorie = QLabel(
    "Catégorie :",
    parent=window
)

label_categorie.move(
    50,
    160
)


categorie = QComboBox(
    parent=window
)

categorie.addItems([
    "Assistance & Demandes generales",
    "Gestion des comptes et mots de passe",
    "Materiel informatique",
    "SAP & Applications metier",
    "Messagerie & Office 365",
    "Logiciels & Applications",
    "Reseau & Connectivite",
    "Securite informatique",
    "Autre"
])

categorie.move(
    200,
    155
)

categorie.resize(
    300,
    30
)


# ============================================================
# 8. TITRE DU TICKET
# ============================================================

label_ticket = QLabel(
    "Titre du ticket :",
    parent=window
)

label_ticket.move(
    50,
    220
)


titre_ticket = QLineEdit(
    parent=window
)

titre_ticket.setPlaceholderText(
    "Ex : Réinitialisation du mot de passe"
)

titre_ticket.move(
    200,
    215
)

titre_ticket.resize(
    300,
    30
)


# ============================================================
# 9. BOUTON PREDIRE
# ============================================================

bouton_predire = QPushButton(
    "PRÉDIRE",
    parent=window
)

bouton_predire.move(
    200,
    280
)

bouton_predire.resize(
    150,
    40
)


# ============================================================
# 10. RESULTAT
# ============================================================

resultat = QLabel(
    "Résultat : --",
    parent=window
)

resultat.move(
    50,
    350
)
resultat.resize(500, 40)


# ============================================================
# 11. PROBABILITE
# ============================================================

probabilite = QLabel(
    "Probabilité : --",
    parent=window
)

probabilite.move(
    50,
    390
)
probabilite.resize(500, 40)


# ============================================================
# 12. CONNECTION DU BOUTON AU MODELE
# ============================================================

bouton_predire.clicked.connect(
    predire_sla
)


# ============================================================
# 13. AFFICHER LA FENETRE
# ============================================================

window.show()


# ============================================================
# 14. LANCER L'APPLICATION
# ============================================================

sys.exit(
    app.exec()
)
