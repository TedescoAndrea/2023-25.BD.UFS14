def coso():
    return "due righe\nseconda riga"

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots' 
    output = coso()  
    snapshot.assert_match(output, 'foo_output.txt')
