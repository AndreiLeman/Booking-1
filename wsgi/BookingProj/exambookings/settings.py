#### exambookings specific parameter settings
############################################################
############################################################

RE_PATTERN_example_com = '[^@]+@example\.com'
EXAMPLE_COM_DOMAIN = 'example.com'
EXAMPLE_SIGNUP_EMAIL_WHITELIST = ['homer@example.com','mrccheng0@gmail.com', 'braeden.nobis@gmail.com', 'connerdunn7399@gmail.com']

RE_PATTERN_cbe_ab_ca = '[^@]+@cbe\.ab\.ca'
CBE_AB_CA_DOMAIN = 'cbe.ab.ca'
PRODUCTION_SIGNUP_EMAIL_WHITELIST = []



############################################################
### ensure following settings are correct for production use
############################################################
############################################################

MAIN_EMAIL_DOMAIN_RE_PATTERN = RE_PATTERN_cbe_ab_ca
MAIN_EMAIL_DOMAIN = CBE_AB_CA_DOMAIN
SIGNUP_EMAIL_WHITELIST = EXAMPLE_SIGNUP_EMAIL_WHITELIST

