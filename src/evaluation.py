import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    f1_score,
    average_precision_score,
    roc_auc_score
)


def evaluate_classification_model(y_true, y_pred, y_pred_proba, model_name="Model"):
    """
    Prints a classification report (precision/recall/F1 per class), F1 and
    PR-AUC as standalone metrics, and displays the confusion matrix and ROC curve.
    """
    print(f"=== Model Evaluation: {model_name} ===")
    print(classification_report(y_true, y_pred))
    print(f"F1 (positive class): {f1_score(y_true, y_pred):.4f}")
    print(f"PR-AUC: {average_precision_score(y_true, y_pred_proba):.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[0])
    
    axes[0].set_title(f"{model_name} - Confusion Matrix")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")

    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    axes[1].plot(fpr, tpr, label=f"AUC = {roc_auc:.4f}")
    axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray")
    axes[1].set_title(f"{model_name} - ROC Curve")
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("True Positive Rate")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def check_overfitting(model, X_train, y_train, X_test, y_test, model_name="Model"):
    """
    Compares ROC-AUC on the training set vs. the test set to check for
    overfitting. A large gap (train >> test) suggests the model has
    memorized the training data rather than learning generalizable patterns.
    """
    train_proba = model.predict_proba(X_train)[:, 1]
    test_proba = model.predict_proba(X_test)[:, 1]

    train_auc = roc_auc_score(y_train, train_proba)
    test_auc = roc_auc_score(y_test, test_proba)

    print(f"=== Overfitting Check: {model_name} ===")
    print(f"Train ROC-AUC: {train_auc:.4f}")
    print(f"Test ROC-AUC:  {test_auc:.4f}")
    print(f"Gap:           {train_auc - test_auc:.4f}")

    if train_auc - test_auc > 0.05:
        print("Warning: gap exceeds 0.05 - possible overfitting.")
    else:
        print("Gap is small - no strong indication of overfitting.")
