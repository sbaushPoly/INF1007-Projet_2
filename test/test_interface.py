import sys
sys.path.insert(0, 'src')
import interface
import pytest

@pytest.mark.parametrize('reponse_recue, intervalle, attendu', [('0', [0,20], None), 
                                                                ('20', [0,20], None), 
                                                                ('5', [0,20], None),
                                                                ('2.2', [1,10], None),
                                                                ('80', [0,20], "La réponse ne se trouve pas dans l'intervalle permise."),
                                                                ('10', [20,40], "La réponse ne se trouve pas dans l'intervalle permise."),
                                                                ('a',[0,20], "La réponse doit être un nombre."),
                                                                ('',[0,20], "Vous devez écrire une réponse.")])

def test_confirmation_reponse(reponse_recue, intervalle, attendu):
    assert interface.confirmation_reponse(reponse_recue, intervalle) == attendu