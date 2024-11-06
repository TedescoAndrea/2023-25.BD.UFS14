def coso():
    return f'''due righe
            seconda riga'''
            
def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    snapshot.assert_match(('function input'), 'foo_output.txt')
