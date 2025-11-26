"""Test minimal des imports pour identifier les problèmes"""
import sys
print(f"Python version: {sys.version}")

try:
    print("\n1. Test import modules.views.__init__")
    import modules.views
    print("   ✓ OK")
except SyntaxError as e:
    print(f"   ✗ SYNTAX ERROR ligne {e.lineno}: {e.msg}")
    print(f"   Fichier: {e.filename}")
    if e.text:
        print(f"   Code: {e.text.strip()}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n2. Test import edit_dish_view directement")
    import modules.views.edit_dish_view
    print("   ✓ OK")
except SyntaxError as e:
    print(f"   ✗ SYNTAX ERROR ligne {e.lineno}: {e.msg}")
    print(f"   Fichier: {e.filename}")
    if e.text:
        print(f"   Code: {e.text.strip()}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n3. Test import fonction render_edit_dish_view")
    from modules.views import render_edit_dish_view
    print("   ✓ OK")
    print(f"   Module: {render_edit_dish_view.__module__}")
except SyntaxError as e:
    print(f"   ✗ SYNTAX ERROR ligne {e.lineno}: {e.msg}")
    print(f"   Fichier: {e.filename}")
    if e.text:
        print(f"   Code: {e.text.strip()}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Tous les imports fonctionnent !")
