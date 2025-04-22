
class transform_to_tokens():
    def __init__(self):
        self.tokens_sequence = []

    def to_token_sequences(self, df):
        for _, row in df.iterrows():
            tokens = []
            for col in df.columns:
                val = row[col]
                token = f"<{col.upper()}_{str(val)}>"
                tokens.append(token)
            self.tokens_sequence.append(" ".join(tokens))
        
        return self.tokens_sequence
        
