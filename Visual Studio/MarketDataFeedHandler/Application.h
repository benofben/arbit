#include <fstream>
using namespace std;

#include "quickfix/Application.h"
#include "quickfix/MessageCracker.h"
#include "quickfix/Session.h"

#include "quickfix/fix42/MarketDataRequest.h"
#include "quickfix/fix42/MarketDataSnapshotFullRefresh.h"
#include "quickfix/fix42/SecurityDefinitionRequest.h"
#include "quickfix/fix42/SecurityDefinition.h"

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

	void onMessage( const FIX42::MarketDataSnapshotFullRefresh& message, const FIX::SessionID& );
	void onMessage( const FIX42::SecurityDefinition& message, const FIX::SessionID& );

	void getSecurities( const FIX::SessionID& sessionID );
	void subscribeFDAX( const FIX::SessionID& sessionID );
	void subscribeOil( const FIX::SessionID& sessionID );
};