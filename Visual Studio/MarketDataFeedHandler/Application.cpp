#include "Application.h"

void Application::onCreate( const FIX::SessionID& sessionID ) 
{
	std::cout << "Created - " << sessionID << std::endl;
}

void Application::onLogon( const FIX::SessionID& sessionID )
{
	std::cout << "Logon - " << sessionID << std::endl;
}

void Application::onLogout( const FIX::SessionID& sessionID )
{
	std::cout << "Logout - " << sessionID << std::endl;
}

void Application::toAdmin( FIX::Message& message, const FIX::SessionID& sessionID) 
{
	// if logon message, add password
	if (message.getHeader().getField(FIX::FIELD::MsgType)=="A")
	{
		char* password="12345678";
		message.getHeader().setField(96, password);
	}

	std::cout << "toAdmin: " << message << std::endl;
}

void Application::toApp( FIX::Message& message, const FIX::SessionID& sessionID )throw( FIX::DoNotSend )
{
	try
	{
		FIX::PossDupFlag possDupFlag;
		message.getHeader().getField( possDupFlag );
		if ( possDupFlag ) throw FIX::DoNotSend();
	}
	catch ( FIX::FieldNotFound& ) {}

	std::cout << std::endl << "OUT: " << message << std::endl;
}

void Application::fromAdmin( const FIX::Message& message, const FIX::SessionID& sessionID) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::RejectLogon ) 
{
	crack( message, sessionID );
	std::cout << "fromAdmin: " << message << std::endl;
}

void Application::fromApp( const FIX::Message& message, const FIX::SessionID& sessionID ) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::UnsupportedMessageType )
{
	crack( message, sessionID );
	std::cout << "fromApp: " << message << std::endl;
}

