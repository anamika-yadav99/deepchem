import pytest

@pytest.mark.torch
def test_featurize():
  """Test that BertFeaturizer.featurize() correctly featurizes all sequences,
  correctly outputs input_ids and attention_mask."""
  from deepchem.feat.bert_tokenizer import BertFeaturizer
  from transformers import BertTokenizerFast
  sequences = [
      '[CLS] D L I P T S S K L V [SEP]', '[CLS] V K K A F F A L V T [SEP]'
  ]
  sequence_long = ['[CLS] D L I P T S S K L V V K K A F F A L V T [SEP]']
  tokenizer = BertTokenizerFast.from_pretrained(
      "Rostlab/prot_bert", do_lower_case=False)
  featurizer = BertFeaturizer(tokenizer)
  feats = featurizer(sequences)
  long_feat = featurizer(sequence_long)
  assert (len(feats) == 2)
  assert (all([len(f) == 3 for f in feats]))
  assert (len(long_feat) == 1)
  assert (len(long_feat[0] == 2))

@pytest.mark.torch
def test_loading():
  """Test that the FASTA loader can load with this featurizer."""
  from transformers import BertModel, BertTokenizerFast
  from deepchem.feat.bert_tokenizer import BertFeaturizer
  from deepchem.data.data_loader import FASTALoader
  import re

  tokenizer = BertTokenizerFast.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
  model = BertModel.from_pretrained("Rostlab/prot_bert")
  featurizer = BertFeaturizer(tokenizer)

  loader = FASTALoader(featurizer = featurizer, legacy = False, auto_add_annotations = True)
  data = loader.create_dataset(input_files = "../../data/tests/uniprot_truncated.fasta")

  assert data.X.shape == (61, 3, 5)
