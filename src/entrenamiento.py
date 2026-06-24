import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, roc_auc_score

print("=== FASE 5: ENTRENAMIENTO DE MODELO IA ===")

# 1. Cargar los datos limpios que generó el pipeline anterior
df = pd.read_csv("data/banco_validado.csv")

# 2. Análisis de Calidad y Correlación (Lo pide la rúbrica)
# Convertir variables categóricas a numéricas (necesario para la matriz y el modelo)
df_numerico = pd.get_dummies(df, drop_first=True)

print("Generando Matriz de Correlación...")
plt.figure(figsize=(10, 8))
sns.heatmap(df_numerico.corr(), annot=False, cmap='coolwarm')
plt.title("Matriz de Correlación")
plt.savefig("data/matriz_correlacion.png") # Guardamos el gráfico para el dashboard/informe
print("✅ Matriz guardada en data/matriz_correlacion.png")

# 3. Preparar los datos para la IA
# Asumiendo que la columna objetivo (si suscribió o no) se llama 'y_yes' después del get_dummies
# Reemplaza 'y_yes' por el nombre real de tu columna objetivo.
X = df_numerico.drop(columns=['deposit_yes']) 
y = df_numerico['deposit_yes']

# Partición de datos (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entrenar el Modelo (Elegimos Random Forest por su buen rendimiento)
print("Entrenando el modelo Random Forest...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 5. Predicciones y Métricas
y_pred = modelo.predict(X_test)
y_prob = modelo.predict_proba(X_test)[:, 1] # Probabilidades para la Curva ROC y Gini

accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)
gini = (2 * roc_auc) - 1 # Fórmula del coeficiente de Gini

print("\n📊 MÉTRICAS DEL MODELO:")
print(f"Accuracy : {accuracy:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"Ind. Gini: {gini:.4f}")

print("\nMatriz de Confusión:")
print(confusion_matrix(y_test, y_pred))