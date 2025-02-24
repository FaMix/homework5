import pandas as pd
from rapidfuzz import process, fuzz
import os

def evaluate_fuzzy_matching(results_csv_path, ground_truth_path, similarity_threshold=70):
    try:
        if not os.path.exists(results_csv_path):
            raise FileNotFoundError(f"The file {results_csv_path} does not exist.")
        if not os.path.exists(ground_truth_path):
            raise FileNotFoundError(f"The file {ground_truth_path} does not exist.")
        
        df_pred = pd.read_excel(results_csv_path)
        df_true = pd.read_excel(ground_truth_path)

        a = 'name_company_1'
        b = 'name_company_2'
        c = 'is_match'
        required_cols = {a, b, c}
        if not required_cols.issubset(df_pred.columns):
            raise ValueError(f"The predictions file must contain the columns: {required_cols}")
        if not required_cols.issubset(df_true.columns):
            raise ValueError(f"The ground truth file must contain the columns: {required_cols}")

        matched_pairs = []
        
        for _, row in df_true.iterrows():
            name1, name2, true_match = row[a], row[b], row[c]

            # Verifica si extractOne devuelve None antes de desempaquetar
            match1 = process.extractOne(name1, df_pred[a], scorer=fuzz.ratio)
            match2 = process.extractOne(name2, df_pred[b], scorer=fuzz.ratio)

            if match1 is None or match2 is None:
                continue  # Si no hay coincidencia, pasa al siguiente

            best_match1, score1, _ = match1
            best_match2, score2, _ = match2

            if score1 >= similarity_threshold and score2 >= similarity_threshold:
                pred_match = df_pred[
                    (df_pred[a] == best_match1) & (df_pred[b] == best_match2)
                ][c].values

                predicted_match = int(pred_match[0]) if len(pred_match) > 0 else 0
                matched_pairs.append((name1, name2, true_match, predicted_match))

        df_merged = pd.DataFrame(matched_pairs, columns=[a, b, 'is_match_true', 'is_match_pred'])

        tp = len(df_merged[(df_merged['is_match_true'] == 1) & (df_merged['is_match_pred'] == 1)])
        fp = len(df_merged[(df_merged['is_match_true'] == 0) & (df_merged['is_match_pred'] == 1)])
        fn = len(df_merged[(df_merged['is_match_true'] == 1) & (df_merged['is_match_pred'] == 0)])
        tn = len(df_merged[(df_merged['is_match_true'] == 0) & (df_merged['is_match_pred'] == 0)])

        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) else 0

        print("\n" + "="*60)
        print("Evaluation with Approximate Name Matching")
        print(f"• Predictions file: {results_csv_path}")
        print(f"• Ground truth file: {ground_truth_path}")
        print(f"• Evaluated pairs (Ground Truth): {len(df_merged)}")
        print(f"• True Positives (TP): {tp}")
        print(f"• False Positives (FP): {fp}")
        print(f"• False Negatives (FN): {fn}")
        print(f"• True Negatives (TN): {tn}")
        print(f"• Precision: {precision:.2%}")
        print(f"• Recall: {recall:.2%}")
        print(f"• F1-Score: {f1:.2%}")
        print(f"• Accuracy: {accuracy:.2%}")
        print("="*60 + "\n")

        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'accuracy': accuracy,
            'TP': tp,
            'FP': fp,
            'FN': fn,
            'TN': tn
        }

    except FileNotFoundError as e:
        print(f"\nError: {str(e)}")
        return None
    except Exception as e:
        print(f"\nError during evaluation: {str(e)}")
        return None

if __name__ == "__main__":
    results_path = "../blocking_excels/company_blocking.xlsx"
    ground_truth_path = "../record_linkage_groundtruth/company_RL_groundtruth.xlsx"

    evaluate_fuzzy_matching(results_path, ground_truth_path)
