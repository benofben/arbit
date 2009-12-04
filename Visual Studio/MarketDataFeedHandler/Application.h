#include "quickfix/Application.h"
#include "quickfix/MessageCracker.h"

class Application :	public FIX::Application, public FIX::MessageCracker
{
private:
	void onCreate( const FIX::SessionID& sessionID );
	void onLogon( const FIX::SessionID& sessionID );
	void onLogout( const FIX::SessionID& sessionID );
	void toAdmin( FIX::Message& message, const FIX::SessionID& sessionID );
	void toApp( FIX::Message&, const FIX::SessionID& ) throw( FIX::DoNotSend );
	void fromAdmin( const FIX::Message& message, const FIX::SessionID& sessionID) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::RejectLogon );
	void fromApp( const FIX::Message& message, const FIX::SessionID& sessionID ) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::UnsupportedMessageType );
};